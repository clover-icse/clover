int main(){
    int x, z;

    // pre-conditions
    x = -100;
    z = -100;

    // loop body
    while(unknown()){
        x = (x + 1) % 5;
        if(z < 4){
            z = z + 1;
        }else{
            z = z % 4;
        }
    }

    // post-condition
    if(z >= 0){
        assert(x == z);
    }
    
}