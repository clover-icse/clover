int main(){
    int x, z;

    // pre-conditions
    x = 1;
    z = 0;

    // loop body
    while(unknown()){
        if(x % 3 == 1){
            z = z + x;
        }else{
            z = z - x;
        }
        x = -x;
    }

    // post-condition
    assert(z >= 0);
    
}