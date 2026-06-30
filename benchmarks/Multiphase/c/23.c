int main(){
    int x, z;

    // pre-conditions
    x = 1000;
    z = 100;

    // loop body
    while(unknown()){
        if((x / 10) < z){
            x = x + 1;
            z = z - 1;
        }else{
            x = x - 1;
            z = z + 1;
        }     
    }

    // post-condition
    assert(z < x);
    
}